import { useEffect, useState } from 'react'
import { useAuth } from '../context/Auth';
import { Link, useNavigate } from 'react-router-dom'
import './Login.css';

function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError(null);

    const data = {
      'email': email,
      'password': password,
    }

    try {
      await login(data);
      navigate('/profile');
    } catch (err) {
      setError(err.message || 'Не удалось войти');
    }
  }

  return (
    <div className="login">
      <h2 className="login__title">Авторизация</h2>

      <p className="login__label">Email</p>
      <input type='text' className="login__input" onChange={(e) => { setEmail(e.target.value) }} />

      <p className="login__label">Пароль</p>
      <input type='password' className="login__input" onChange={(e) => { setPassword(e.target.value) }} />

      {error && <p className="login__error">{error}</p>}

      <button onClick={handleLogin} className="btn-login">Вход</button>

      <Link to="/registration" className="login__register">Регистрация</Link>
    </div>
  )
}

export default Login;