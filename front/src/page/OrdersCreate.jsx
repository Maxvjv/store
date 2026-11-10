import { useState, useEffect } from 'react'
import {Link, useParams} from 'react-router-dom';
import {useAuth} from '../context/Auth';


function OrdersCreate(){
const { user, addOrders,getAddress} = useAuth();
  const [shippingAddressId, setShippingAddressId] = useState('');
  const [contactphone, setContactphone] = useState('');
  const [addresses, setAddresses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }

    const loadAddresses = async () => {
      try {
        const data = await getAddress(user);
        setAddresses(data || []);
        
        if (Array.isArray(data) && data.length > 0) {
          setShippingAddressId(String(data[0].id));
        } else {
          setShippingAddressId('');
        }
      } catch (err) {
        console.error(err);
        setError('Не удалось загрузить адреса. Проверьте авторизацию.');
      } finally {
        setLoading(false);
      }
    };

    loadAddresses();
  }, [user, getAddress]);

  const handleOrders = async (e) => {
    e.preventDefault();

    if (!shippingAddressId) {
      alert('Пожалуйста, выберите адрес доставки');
      return;
    }

    const payload = {
      shipping_address: Number(shippingAddressId),
      contact_phone: contactphone.trim(),
    };

    try {
      await addOrders(payload);
      alert('Заказ успешно оформлен!');
    } catch (err) {
      console.error(err);
      const msg = err.message || 'Ошибка при оформлении заказа';
      alert(msg);
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '20px' }}>Загрузка адресов...</div>;
  if (error) return <div style={{ color: 'red', padding: '10px', textAlign: 'center' }}>{error}</div>;
  if (addresses.length === 0)
    return (
      <div style={{ padding: '20px', color: '#666', textAlign: 'center' }}>
        У вас нет сохранённых адресов. Добавьте адрес в профиле, чтобы оформить заказ.
      </div>
    );

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h2>Оформление заказа</h2>

      <form onSubmit={handleOrders}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Адрес доставки</label>
          <select
            value={shippingAddressId}
            onChange={(e) => setShippingAddressId(e.target.value)}
            style={{
              width: '100%',
              padding: '8px 12px',
              fontSize: '14px',
              borderRadius: '4px',
              border: '1px solid #ccc',
            }}
          >
            {addresses.map((addr) => (
              <option key={addr.id} value={addr.id}>
                {addr.address || addr.full_address || `${addr.country},${addr.city},
                                                       ${addr.street},${addr.house},
                                                       ${addr.apartment},${addr.postal_code}`}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '6px', fontWeight: 'bold' }}>Контактный телефон</label>
          <input
            type="text"
            value={contactphone}
            onChange={(e) => setContactphone(e.target.value)}
            placeholder="+7 (999) 000-00-00"
            style={{
              width: '100%',
              padding: '8px 12px',
              fontSize: '14px',
              borderRadius: '4px',
              border: '1px solid #ccc',
            }}
          />
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '16px',
          }}
        >
          Оформить заказ
        </button>
      </form>
    </div>
  );
}
export default OrdersCreate;