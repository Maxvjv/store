import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Review.css';

function Review() {
  const { prodId } = useParams();
  const { user, addReview } = useAuth();

  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleReview = async (e) => {
    e.preventDefault();
    setError(null);

    if (!rating) {
      setError('Поставьте оценку — от 1 до 5 звёзд');
      return;
    }

    try {
      const data = {
        rating: rating,
        comment: comment,
      };
      await addReview(prodId, data);
      navigate(-1);
    } catch (err) {
      setError(err.message || 'Не удалось сохранить отзыв');
    }
  };

  if (!user) {
    return (
      <div className="review">
        <h2 className="review__title">Оставить отзыв</h2>
        <p className="review__subtitle">
          Чтобы оставить отзыв, нужно войти в аккаунт.
        </p>
      </div>
    );
  }

  return (
    <form className="review" onSubmit={handleReview}>
      <h2 className="review__title">Оставить отзыв</h2>
      <p className="review__subtitle">Расскажите, что думаете о товаре</p>

      <label className="review__label">Оценка</label>
      <div className="review__stars">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            type="button"
            key={star}
            className={`review__star ${rating >= star ? 'review__star--active' : ''}`}
            onClick={() => setRating(star)}
          >
            ★
          </button>
        ))}
      </div>

      <label className="review__label">Комментарий</label>
      <textarea
        className="review__textarea"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows="4"
      />

      {error && <p className="review__error">{error}</p>}

      <button type="submit" className="btn-primary">Сохранить отзыв</button>
      <p className="review__hint">Отзыв появится в списке после сохранения</p>
    </form>
  );
}

export default Review;