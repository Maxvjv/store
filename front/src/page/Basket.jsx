import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Basket.css';

function Basket() {
  const { user, getBasket, addBasket, deleteBasket } = useAuth();
  const [listbasket, setListbasket] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getBasket();
        const list = Array.isArray(data)
          ? data
          : (data && Array.isArray(data.items)) ? data.items : [];
        setListbasket(list);
      } catch (err) {
        console.error('Не удалось загрузить корзину:', err);
        setListbasket([]);
        setError(err.message || 'Не удалось загрузить корзину');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user]);

  const handleDelete = async (id) => {
    try {
      await deleteBasket(id);                    
      const updated = await getBasket();         

      const list = Array.isArray(updated)
        ? updated
        : (updated && Array.isArray(updated.items)) ? updated.items : [];

      setListbasket(list);                      
    } catch (err) {
      console.error('Ошибка удаления:', err);
      setListbasket((prev) => prev.filter((b) => b.product_id !== id));
    }
  };

  const handleAdd = async (id) => {
    try {
      await addBasket(id);
      const updated = await getBasket();
      const list = Array.isArray(updated)
        ? updated
        : (updated && Array.isArray(updated.items)) ? updated.items : [];
      setListbasket(list);
    } catch (err) {
      console.error('Ошибка добавления:', err);
    }
  };

  const totalSum = listbasket.reduce((sum, bask) => sum + Number(bask.line_total || 0), 0);

  if (loading) return <div className="basket__loading">Загрузка...</div>;
  if (error) return <div className="basket__error">{error}</div>;

  return (
    <div className="basket">
      <h2 className="basket__title">Корзина</h2>

      {listbasket.length === 0 ? (
        <div className="basket__empty">
          Корзина пуста — загляните в <Link to="/catalog">каталог</Link> и добавьте товары 😊
        </div>
      ) : (
        <>
          <div className="basket__grid">
            {listbasket.map((bask) => (
              <div className="basket-card" key={bask.id}>
                <p className="basket-card__name">{bask.product_name}</p>

                <div className="basket-card__price-row">
                  <span className="basket-card__unit-price">
                    {bask.final_unit_price} ₽ за шт.
                  </span>
                  <span className="basket-card__total">
                    {bask.line_total} ₽
                  </span>
                </div>

                <div className="basket-card__controls">
                  <button
                    className="btn-qty"
                    onClick={() => handleDelete(bask.product_id)}
                    aria-label="Убрать одну штуку"
                  >
                    −
                  </button>
                  <span className="basket-card__qty">{bask.quantity} шт.</span>
                  <button
                    className="btn-qty"
                    onClick={() => handleAdd(bask.product_id)}
                    aria-label="Добавить одну штуку"
                  >
                    +
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="basket__summary">
            <div>
              <p className="basket__total-label">Итого к оплате</p>
              <p className="basket__total-value">{totalSum} ₽</p>
            </div>
            <Link to="/basket/orderscreate" className="basket__checkout-btn">
              Оформить заказ
            </Link>
          </div>
        </>
      )}
    </div>
  );
}

export default Basket;