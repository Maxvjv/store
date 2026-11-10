import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './ProductDetail.css';

function ProductDetail() {
  const { user, addFavorites, addBasket } = useAuth();
  const { getProductDetail, getFavorites, getBasket } = useAuth();
  const { prodId } = useParams();
  const [proddet, setProddet] = useState(null);

  const [inFavorites, setInFavorites] = useState(false);
  const [inBasket, setInBasket] = useState(false);

  useEffect(() => {
    const load = async () => {
      const data = await getProductDetail(prodId)
      setProddet(data)
      console.log(data)
    }
    load()
  }, [prodId]);

  useEffect(() => {
    if (!user || !proddet) return;

    const check = async () => {
      try {
        const favs = await getFavorites();
        const favList = Array.isArray(favs) ? favs : (favs.product || []);
        setInFavorites(favList.some((f) => f.id === Number(prodId)));

        const basket = await getBasket(user);
        const basketList = Array.isArray(basket) ? basket : (basket.items || basket.products || []);
        setInBasket(basketList.some((b) => b.product_id === Number(prodId)));
      } catch (err) {
        console.error('Не удалось проверить корзину/избранное:', err);
      }
    };
    check();
  }, [user, proddet, prodId, getFavorites, getBasket]);

  const handleAddFavorites = async () => {
    await addFavorites(proddet.id);
    setInFavorites(true);
  };

  const handleAddBasket = async () => {
    await addBasket(proddet.id);
    setInBasket(true);
  };

  if (!proddet) {
    return <div className="product-detail__loading">Загрузка товара...</div>;
  }

  return (
    <div className="product-detail">
      <h2 className="product-detail__title">{proddet.name}</h2>

      <div className="product-detail__price">{proddet.price} ₽</div>
      <p className="product-detail__meta">На складе: {proddet.stock} шт.</p>
      <p className="product-detail__meta">
        Рейтинг: <span className="product-detail__rating">★</span> {proddet.average_rating}
      </p>

      <div className="product-detail__section">
        <h3 className="product-detail__subtitle">Описание</h3>
        <p className="product-detail__desc">
          {proddet.description || 'Описание отсутствует'}
        </p>
      </div>

      {user && (
        <div className="product-detail__actions">
          <button
            onClick={handleAddBasket}
            disabled={inBasket}
            className={inBasket ? 'btn-added' : 'btn-primary'}
          >
            {inBasket ? '✓ Уже в корзине' : 'В корзину'}
          </button>

          <button
            onClick={handleAddFavorites}
            disabled={inFavorites}
            className={inFavorites ? 'btn-added-outline' : 'btn-outline'}
          >
            {inFavorites ? '♥ Уже в избранном' : 'В избранное'}
          </button>
        </div>
      )}

      <div className="product-detail__links">
        {user && (
          <Link to={`/review/${proddet.id}`} className="detail-link">
            Оставить отзыв →
          </Link>
        )}
        <Link to={`/reviewlist/${proddet.id}`} className="detail-link">
          Все отзывы на товар →
        </Link>
      </div>
    </div>
  );
}

export default ProductDetail;