const login_api = async (username, password, success, fail) => {
  const response = await fetch(`/api/token/`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  const text = await response.text();
  if (response.status === 200) {
    success(JSON.parse(text));
  } else {
    Object.entries(JSON.parse(text)).forEach(([key, value]) => {
      fail(`${key}: ${value}`);
    });
  }
};

const get_analysis_api = async (pageNo = '', success, fail) => {
  const token = await localStorage.getItem('reynoldsToken');
  if (token === null) {
    window.location = '/login';
    return [];
  }
  const response = await fetch('/api/analysis/', {
    method: 'GET',
    headers: {
      'Content-Type': 'Application/JSON',
      Authorization: `Bearer ${token}`,
    },
  });
  const text = await response.text();
  if (response.status === 401) {
    window.location = '/login';
    return [];
  }
  if (response.status === 200) {
    success(JSON.parse(text));
  } else {
    Object.entries(JSON.parse(text)).forEach(([key, value]) => {
      fail(`${key}: ${value}`);
    });
  }
};

const post_analysis_api = async (data, success) => {
  const token = await localStorage.getItem('reynoldsToken');
  if (token === null) {
    window.location = '/login';
    return [];
  }
  const response = await fetch(`/api/analysis/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'Application/JSON',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  const text = await response.text();
  if (response.status === 401) {
    window.location = '/login';
    return [];
  }
  if (response.status === 201) {
    success(JSON.parse(text));
  } else {
    Object.entries(JSON.parse(text)).forEach(([key, value]) => {
      fail(`${key}: ${value}`);
    });
  }
};

const put_analysis_api = async (analysisId, data, success) => {
  const token = await localStorage.getItem('reynoldsToken');
  if (token === null) {
    window.location = '/login';
    return [];
  }
  const response = await fetch(`/api/analysis/${analysisId}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'Application/JSON',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  const text = await response.text();
  if (response.status === 401) {
    window.location = '/login';
    return [];
  }
  if (response.status === 200) {
    success(JSON.parse(text));
  } else {
    Object.entries(JSON.parse(text)).forEach(([key, value]) => {
      fail(`${key}: ${value}`);
    });
  }
};

const delete_analysis_api = async (analysisId, success) => {
  const token = await localStorage.getItem('reynoldsToken');
  if (token === null) {
    window.location = '/login';
    return [];
  }
  const response = await fetch(`/api/analysis/${analysisId}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'Application/JSON',
      Authorization: `Bearer ${token}`,
    },
  });

  const text = await response.text();

  if (response.status === 401) {
    window.location = '/login';
    return [];
  }

  if (response.status === 410 || response.status === 204) {
    success();
  } else {
    Object.entries(JSON.parse(text)).forEach(([key, value]) => {
      fail(`${key}: ${value}`);
    });
  }
};
