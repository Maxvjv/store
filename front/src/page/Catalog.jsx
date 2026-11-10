import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Catalog.css';

function Catalog() {
  const { catId } = useParams();
  const { getCategory } = useAuth();
  const [category, setCategory] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await getCategory()
      setCategory(data)
      console.log(data)
    }
    load()
  }, []);

  return (
    <div className="catalog">
      <h2 className="catalog__title">Каталог</h2>

      {category.length === 0 ? (
        <div className="catalog__empty">
          Категорий пока нет — загляните позже 😊
        </div>
      ) : (
        <div className="catalog__grid">
          {category.map((cat) => (
            <div className="category-card" key={cat.id}>
              <Link to={`/catalog/${cat.id}`} className="category-card__name">
                {cat.name}
              </Link>
              {cat.description && (
                <p className="category-card__desc">{cat.description}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Catalog;