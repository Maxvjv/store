import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Favorites.css';

function Favorites() {
  const { user, getFavorites, deleteFavorites } = useAuth();
  const [favorite, setFavorites] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await getFavorites()
      setFavorites(Array.isArray(data) ? data : [])
      console.log(data)
    }
    load()
  }, []);

  // Обновление списка после удаления
const handleDelete = async (id) => {
    try {
      await deleteFavorites(id);                 
      const updated = await getFavorites();      
      const list = Array.isArray(updated)
        ? updated
        : (updated && Array.isArray(updated.product)) ? updated.product : [];

      setFavorites(list);                        
    } catch (err) {
      console.error('Ошибка удаления:', err);
      setFavorites((prev) => prev.filter((f) => f.id !== id));
    }
  };

  return (
    <div className="favorites">
      <h2 className="favorites__title">Избранное</h2>

      {favorite.length === 0 ? (
        <div className="favorites__empty">
          В избранном пока пусто — загляните в <Link to="/catalog">каталог</Link> и добавьте что-нибудь 💛
        </div>
      ) : (
        <div className="favorites__grid">
          {favorite.map((fat) => (
            <div className="favorite-card" key={fat.id}>
              <Link to={`/product/${fat.id}`} className="favorite-card__name">
                {fat.name}
              </Link>

              {fat.description && (
                <p className="favorite-card__desc">{fat.description}</p>
              )}

              <button
                className="favorite-card__remove"
                onClick={() => handleDelete(fat.id)}
              >
                Убрать из избранного
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Favorites;