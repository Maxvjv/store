import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './ProductList.css';

function ProductList() {
  const { getProduct } = useAuth();
  const { catId } = useParams();
  const [prodlist, setProdlist] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await getProduct(catId)
      setProdlist(data.products)
      console.log(data.products)
    }
    load()
  }, [catId]);

  return (
    <div className="products">
      <h2 className="products__title">Товары</h2>

      {prodlist.length === 0 ? (
        <div className="products__empty">
          В этой категории пока пусто — загляните в другую 😊
        </div>
      ) : (
        <div className="products__grid">
          {prodlist.map((product) => (
            <div className="product-card" key={product.id}>
              <Link to={`/catalog/${catId}/${product.id}`} className="product-card__link">
                {product.name}
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ProductList;