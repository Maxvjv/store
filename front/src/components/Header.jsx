import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/Auth";
import "./Header.css";

import { FiUser, FiHeart, FiShoppingBag, FiGrid } from "react-icons/fi";

function Header() {
  const { user, logOut } = useAuth();

  return (
    <header className="header">
      <Link to="/" className="header__logo">
        ФруктовыйМикс
      </Link>

      <nav className="header__nav">
        {/* Каталог теперь с иконкой */}
        <Link to="/catalog" className="nav-link">
          <FiGrid size={18} /> Каталог
        </Link>

        {user && (
          <Link to="/profile" className="nav-link">
            <FiUser size={18} /> Профиль
          </Link>
        )}

        <Link to="/favorites" className="nav-link">
          <FiHeart size={18} color="#ff4d4d" /> Избранное
        </Link>

        <Link to="/basket" className="nav-link">
          <FiShoppingBag size={18} /> Корзина
        </Link>

        {!user && (
          <Link to="/login" className="btn-login">Войти</Link>
        )}

        {user && (
          <button onClick={logOut} className="btn-logout">
            Выход
          </button>
        )}
      </nav>
    </header>
  );
}

export default Header;