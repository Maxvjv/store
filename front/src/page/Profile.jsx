import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Profile.css';

function Profile() {
  const { getProfile } = useAuth();
  const [profile, setProfile] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await getProfile()
      setProfile(data)
      console.log(data)
    }
    load()
  }, []);

  return (
    <div className="profile">
      <h2 className="profile__title">Профиль пользователя</h2>

      <div className="profile__grid">
        <span className="profile__label">Имя</span>
        <p className="profile__value">{profile.first_name || 'Не указано'}</p>

        <span className="profile__label">Фамилия</span>
        <p className="profile__value">{profile.last_name || 'Не указано'}</p>

        <span className="profile__label">Эл. почта</span>
        <p className="profile__value">{profile.email || 'Не указана'}</p>

        <span className="profile__label">Телефон</span>
        <p className="profile__value">{profile.phone || 'Не указан'}</p>
      </div>

      <div className="profile__links">
        <Link to="/myorders" className="profile-card">
          <span className="profile-card__title">
            Мои заказы
            <span className="profile-card__arrow">→</span>
          </span>
          <span className="profile-card__desc">История покупок и статусы доставки</span>
        </Link>

        <Link to="/address" className="profile-card">
          <span className="profile-card__title">
            Мои адреса
            <span className="profile-card__arrow">→</span>
          </span>
          <span className="profile-card__desc">Адреса доставки для новых заказов</span>
        </Link>
      </div>
    </div>
  )
}

export default Profile;