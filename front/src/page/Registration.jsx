import { useState, useEffect } from 'react'
import { useAuth } from '../context/Auth';
import { useNavigate } from 'react-router-dom';
import './Registration.css';

function Registration() {
  const { user, registrationUser } = useAuth()

  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [phone, setPhone] = useState('')

  const navigate = useNavigate();

  const handleRegistr = async () => {
    const data = {
      'email': email,
      'password': password,
      'first_name': firstName,
      'last_name': lastName,
      'phone': phone,
    }
    await registrationUser(data)
    navigate('/login')
  }

  return (
    <div className="registration">
      <h2 className="registration__title">Регистрация</h2>

      <p className="registration__label">Имя</p>
      <input type='text' value={firstName} className="registration__input" onChange={(e) => { setFirstName(e.target.value) }} />

      <p className="registration__label">Фамилия</p>
      <input type='text' value={lastName} className="registration__input" onChange={(e) => { setLastName(e.target.value) }} />

      <p className="registration__label">Email</p>
      <input type='text' value={email} className="registration__input" onChange={(e) => { setEmail(e.target.value) }} />

      <p className="registration__label">Пароль</p>
      <input type='password' value={password} className="registration__input" onChange={(e) => { setPassword(e.target.value) }} />

      <p className="registration__label">Телефон</p>
      <input type='text' value={phone} className="registration__input" onChange={(e) => { setPhone(e.target.value) }} />

      <button onClick={() => { handleRegistr() }} className="btn-primary">Сохранить</button>
    </div>
  )
}

export default Registration