import { useState, useEffect } from 'react';
import { Link,useNavigate } from 'react-router-dom';
import { useAuth } from '../context/Auth';

function Address() {
  const { user, getAddress, deleteAddress} = useAuth();
  const [listadr, setListadr] = useState([]);      
  const [loading, setLoading] = useState(true);     
  const [error, setError] = useState(null);         
  const navigate = useNavigate();

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getAddress(user);
        const addresses = Array.isArray(data) ? data : [];

        setListadr(addresses);
      } catch (err) {
        console.error(err);
        setError(err.message || 'Не удалось загрузить адреса');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user, getAddress]);

  if (loading) return <div style={{ textAlign: 'center', padding: '20px' }}>Загрузка...</div>;
  if (error) return <div style={{ color: 'red', textAlign: 'center', padding: '20px' }}>{error}</div>;


//Обновление списка после удаления
 const handleDelete = async (id) => {
    try {
      await deleteAddress(id);                
      const updated = await getAddress();      
      setListadr(updated);                     
      navigate('/address')                    
    } catch (err) {
      console.error('Ошибка удаления:', err);
    }
  };

return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        marginBottom: '24px' 
      }}>
        <Link 
          to="/address/addresscreate"
          style={{
            padding: '10px 20px',
            backgroundColor: '#0d47a1',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: '6px',
            fontWeight: '600',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#0b3d8a'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#0d47a1'}
        >
          Добавить адрес
        </Link>
      </div>

      <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', gap: '16px' }}>
        {listadr.length === 0 && (
          <div style={{ width: '100%', textAlign: 'center', color: '#666' }}>
            У вас пока нет сохранённых адресов
          </div>
        )}

        {listadr.map((adr) => (
          <div
            key={adr.id}
            style={{
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
              padding: '16px',
              backgroundColor: '#fff',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
              minWidth: '200px',
              maxWidth: '300px',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px'
            }}
          >
            <p style={{ margin: 0, fontWeight: 'bold', color: '#333' }}>{adr.country}</p>
            <p style={{ margin: 0, color: '#555' }}>{adr.city}</p>
            <p style={{ margin: 0, color: '#555' }}>{adr.street}</p>
            <p style={{ margin: 0, color: '#555' }}>{adr.house}{adr.apartment ? `, кв. ${adr.apartment}` : ''}</p>
            <p style={{ margin: 0, color: '#555', fontSize: '0.9rem' }}>{adr.postalcode}</p>

            <Link 
              to={`/address/update/${adr.id}`} 
              style={{
                display: 'block',
                marginTop: '12px',
                padding: '8px',
                textAlign: 'center',
                color: '#0d47a1',
                textDecoration: 'none',
                border: '1px solid #0d47a1',
                borderRadius: '4px'
              }}
            >
              Редактировать адрес
            </Link>
            <button
             type="button"
                 onClick={() => handleDelete(adr.id)}
                    style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    backgroundColor: 'transparent',
                    color: '#d93636',
                    border: '1px solid #d93636',
                    padding: '6px 12px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '13px',
                    transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                    e.target.style.backgroundColor = '#d93636';
                    e.target.style.color = '#fff';
                }}
                onMouseLeave={(e) => {
                    e.target.style.backgroundColor = 'transparent';
                    e.target.style.color = '#d93636';
                }}
                >
                🗑️ Удалить адрес
                </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Address;