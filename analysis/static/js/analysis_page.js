'use strict';
const e = React.createElement;

function App() {
  const [list, setList] = React.useState([]);
  const [count, setCount] = React.useState(0);
  const [pages, setPages] = React.useState([]);
  const [page, setPage] = React.useState(0);
  const [showModal, setShowModal] = React.useState(false);
  const [modalDescription, setModalDescription] = React.useState('');
  const [itemId, setItemId] = React.useState(null);
  const [error, setError] = React.useState('');
  const [viscosity, setViscosity] = React.useState(0);
  const [diameter, setDiameter] = React.useState(0);
  const [flow, setFlow] = React.useState(0);

  const success = (data) => {
    setList(data);
  };

  const logout = async (e) => {
    await localStorage.setItem('reynoldsToken', null);
    window.location = '/login';
  };

  const getData = () => {
    get_analysis_api(page, success, (text) => {
      console.log('Error: ', text);
    });
  };

  const newAnalysis = () => {
    setModalDescription('New Analysis');
    setItemId(null);
    setViscosity('');
    setDiameter('');
    setFlow('');
    setError('');
    setShowModal(true);
    const itemInput = document.getElementById('itemInput');
    setTimeout(() => {
      itemInput && itemInput.focus();
    }, 1);
  };

  const editAnalysis = (data) => {
    setModalDescription('Update Analysis');
    setItemId(data.id);
    setViscosity(data.viscosity);
    setDiameter(data.diameter);
    setFlow(data.flow);
    setError('');
    setShowModal(true);
    const itemInput = document.getElementById('itemInput');
    setTimeout(() => {
      itemInput && itemInput.focus();
    }, 1);
  };

  const saveAnalysis = (e) => {
    e.preventDefault();
    setError('');
    console.log('saving new', viscosity, diameter, flow);
    if (viscosity * diameter * flow === 0)
      setError('Please enter item viscosity, diameter and flow');
    else {
      if (itemId === null)
        post_analysis_api(
          {
            viscosity: viscosity,
            diameter: diameter,
            flow: flow,
          },
          () => {
            getData();
          }
        );
      else
        put_analysis_api(
          itemId,
          {
            viscosity: viscosity,
            diameter: diameter,
            flow: flow,
          },
          () => {
            getData();
          }
        );
      setShowModal(false);
    }
  };

  const deleteAnalysis = (analysisId) => {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!',
    }).then((result) => {
      if (result.isConfirmed) {
        delete_analysis_api(analysisId, () => {
          Swal.fire({
            title: 'Deleted!',
            text: 'Your analysis has been deleted!',
            icon: 'success',
            timer: 1000,
          });
          getData();
        });
      }
    });
  };

  const keyDownHandler = (e) => {
    if (e.which === 27) setShowModal(false);
  };

  React.useEffect(() => {
    getData();
  }, [page]);

  return (
    <div onKeyDown={keyDownHandler}>
      <div
        style={{ background: '#00000060' }}
        className={'modal ' + (showModal ? ' show d-block' : ' d-none')}
        tabIndex='-1'
        role='dialog'
      >
        <div className='modal-dialog shadow'>
          <form method='post'>
            <div className='modal-content'>
              <div className='modal-header'>
                <h5 className='modal-title'>{modalDescription}</h5>
                <button
                  type='button'
                  className='btn-close'
                  onClick={() => {
                    setShowModal(false);
                  }}
                  aria-label='Close'
                ></button>
              </div>
              <div className='modal-body'>
                <label>Kinematic Viscosity (St)</label>
                <div className='form-group'>
                  <input
                    type='number'
                    className='form-control'
                    placeholder='Kinematic Viscosity (St)'
                    value={viscosity}
                    onChange={(e) => {
                      setViscosity(e.target.value);
                    }}
                    name='viscosity'
                  />
                </div>
                <label style={{ marginTop: '1em' }}>Pipe Diameter (m)</label>
                <div className='form-group'>
                  <input
                    type='number'
                    className='form-control'
                    placeholder='Pipe Diameter (m)'
                    value={diameter}
                    onChange={(e) => {
                      setDiameter(e.target.value);
                    }}
                    name='diameter'
                  />
                </div>
                <label style={{ marginTop: '1em' }}>
                  Volumetric Flow Rate (m3/s)
                </label>
                <div className='form-group'>
                  <input
                    type='number'
                    className='form-control'
                    value={flow}
                    onChange={(e) => {
                      setFlow(e.target.value);
                    }}
                    placeholder='Volumetric Flow Rate (m3/s)'
                    name='flow'
                  />
                </div>
                <small className='form-text text-muted'>{error}</small>
              </div>
              <div className='modal-footer'>
                <button
                  type='button'
                  className='btn btn-secondary'
                  onClick={() => {
                    setShowModal(false);
                  }}
                  data-bs-dismiss='modal'
                >
                  Close
                </button>
                <button
                  type='submit'
                  className='btn btn-primary'
                  onClick={saveAnalysis}
                >
                  Save
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <div
        style={{
          maxWidth: '800px',
          margin: 'auto',
          marginTop: '1em',
          marginBottom: '1em',
          padding: '1em',
        }}
        className='shadow'
      >
        <div style={{ display: 'flex', flexDirection: 'row' }}>
          <span>Reynolds Number App</span>
          <a
            className='btn btn-light'
            style={{ marginLeft: 'auto' }}
            onClick={logout}
          >
            Logout
          </a>
        </div>
      </div>
      <div
        style={{
          maxWidth: '800px',
          margin: 'auto',
          marginTop: '1em',
          marginBottom: '1em',
          padding: '1em',
        }}
        className='shadow'
      >
        <div
          style={{ display: 'flex', flexDirection: 'row', marginBottom: '5px' }}
        >
          {pages.length > 0 && (
            <nav className='d-lg-flex justify-content-lg-end dataTables_paginate paging_simple_numbers'>
              <ul className='pagination'>
                <li
                  className={'page-item ' + (page === 0 ? 'disabled' : '')}
                  onClick={(e) => {
                    e.preventDefault();
                    setPage(Math.max(page - 1, 0));
                  }}
                >
                  <a className='page-link' href='#' aria-label='Previous'>
                    <span aria-hidden='true'>«</span>
                  </a>
                </li>
                {pages.map((el) => (
                  <li
                    key={'page' + el.page}
                    onClick={(e) => {
                      setPage(el.page);
                    }}
                    className={
                      'page-item ' + (page === el.page ? 'active' : '')
                    }
                  >
                    <a className='page-link' href='#'>
                      {el.name}
                    </a>
                  </li>
                ))}
                <li
                  className={
                    'page-item ' + (page === pages.length - 1 ? 'disabled' : '')
                  }
                  onClick={(e) => {
                    setPage(Math.min(page + 1, pages.length - 1));
                  }}
                >
                  <a className='page-link' href='#' aria-label='Next'>
                    <span aria-hidden='true'>»</span>
                  </a>
                </li>
              </ul>
            </nav>
          )}
          <a
            className='btn btn-light'
            style={{ marginLeft: 'auto' }}
            onClick={newAnalysis}
          >
            New Analysis
          </a>
        </div>
        <table className='table table-hover caption-top'>
          <thead className='table-light'>
            <tr>
              <th>Viscosity (St)</th>
              <th>Diameter (m)</th>
              <th>Flow (m³/s)</th>
              <th>Reynolds Number</th>
              <th>Regime</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {list.map((row) => (
              <tr key={row.id}>
                <td>{row.viscosity}</td>
                <td>{row.diameter}</td>
                <td>{row.flow}</td>
                <td>{row.reynolds_number.toExponential(2)}</td>
                <td>{row.reynolds_number_regime}</td>
                <td>
                  <a
                    className='btn btn-light'
                    style={{ marginLeft: 'auto' }}
                    onClick={(e) => {
                      editAnalysis(row);
                    }}
                  >
                    Edit
                  </a>{' '}
                  <a
                    className='btn btn-light'
                    style={{ marginLeft: 'auto' }}
                    onClick={(e) => {
                      deleteAnalysis(row.id);
                    }}
                  >
                    Delete
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(e(App), domContainer);
