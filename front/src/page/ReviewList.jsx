import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './ReviewList.css';

function ReviewList() {
  const { getReviewList } = useAuth();
  const { prodId } = useParams();
  const [revlist, setRevlist] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await getReviewList(prodId)
      setRevlist(data.reviews)
      console.log(data.reviews)
    }
    load()
  }, [prodId]);

  return (
    <div className="reviews">
      <h2 className="reviews__title">Отзывы на товар</h2>
      <p className="reviews__subtitle">
        Что покупатели думают об этом товаре
      </p>

      {revlist.length === 0 ? (
        <div className="reviews__empty">
          Отзывов пока нет — станьте первым, кто поделится мнением 😊
        </div>
      ) : (
        <div className="reviews__grid">
          {revlist.map((rev) => (
            <div className="review-card" key={rev.id}>
              <div className="review-card__head">
                <p className="review-card__author">
                  {rev.user.first_name} {rev.user.last_name}
                </p>
                <span className="review-card__rating">
                  {'★'.repeat(rev.rating)}
                </span>
              </div>
              <p className="review-card__text">{rev.comment}</p>
            </div>
          ))}
        </div>
      )}

      <Link to={`/catalog/catalogId/${prodId}`} className="reviews__back">
        ← Назад к товару
      </Link>
    </div>
  );
}

export default ReviewList;