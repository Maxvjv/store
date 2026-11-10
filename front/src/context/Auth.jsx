import { createContext, useContext, useEffect, useState } from "react";
import { Link,useNavigate } from 'react-router-dom';


const Auth = createContext();

    export function AuthProvider({children}) {
    const [user,setUser] = useState(null);
    const [favorites,setFavorites] = useState([]);
	const [loadingAuth, setLoadingAuth] = useState(true);

const login = async (data) => {
    const response = await fetch('/auth/login',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify(data)
        }
    );

    if (!response.ok) {
        throw new Error('Неверный логин или пароль');
    }

    const info = await response.json();
    console.log(info);
    localStorage.setItem('access_token', info.access_token);
    setUser(info);
    return info;
}
// Отмена авторизации
const logOut = () => {
    localStorage.removeItem('access_token'); 
    setUser(null);                        
  };


// Восстановление сессии при загрузке страницы
useEffect(() => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    setLoadingAuth(false);
    return;
  }

  const restore = async () => {
    try {
      const response = await fetch('/users/list/me', {
        method: 'GET',
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);          
      } else {
        localStorage.removeItem('access_token');  
        setUser(null);
      }
    } catch (err) {
      console.error('Не удалось восстановить сессию:', err);
    } finally {
      setLoadingAuth(false);
    }
  };

  restore();
}, []);



//Регистрация
const registrationUser = async (data) =>{

  const response = await fetch('/users/registration',
      {method:'POST',
        headers: {'Content-Type':'application/json',
        'accept':'application/json'},
        body : JSON.stringify(data)
      }
    )
      console.log(data)
    return await response.json();
} 
// Каталог
   const getCategory = async () => {
   const response = await fetch('/category/list/',
    {method:'GET',
          headers: {'Content-Type':'application/json',
          'accept':'application/json'},
        })
    console.log(response)
    const info = await response.json()
    console.log(info)
    return info
   }


//Продукты категории
   const getProduct = async (catId) => {
    const response = await fetch(`/category/list/${catId}`,
      {method:'GET',
          headers: {'Content-Type':'application/json',
          'accept':'application/json'},
        })
    console.log(response)
    const info = await response.json()
    console.log(info)
    return info
   }

// Детальная информация о продукте
   const getProductDetail = async (prodId) => {
    const response = await fetch(`/product/list/${prodId}`,
      {method:'GET',
          headers: {'Content-Type':'application/json',
          'accept':'application/json'},
        })
    console.log(response)
    const info = await response.json()
    console.log(info)
    return info
   }

   
//Профиль пользователя
const getProfile = async () => {
   const token = localStorage.getItem('access_token');
  if (!token) {
    console.warn('Токен не найден');
    return null;
  }

  try {
    const response = await fetch('/users/list/me',
    { 
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': `Bearer ${token}` 
      }
    });

    if (response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_profile');
      alert('Сессия истекла, войдите снова');
      return null;
    }

    const user = await response.json();
    console.log('Профиль пользователя:', user);

    localStorage.setItem('user_profile', JSON.stringify(user));
    return user;
  } catch (err) {
    console.error('Ошибка запроса профиля:', err);
    return null;
  }
};

//Добавление в избранное
const addFavorites = async (prodId) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch('/favorite/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ product_id: prodId})
  });
  return await response.json();
};

const deleteFavorites = async (prodId) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch(`/favorite/delete/${prodId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },  
  });
  if (response.status === 204) {
    return {}; 
  }
  return await response.json();
};

// Получение списка избранного
const getFavorites = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('Требуется авторизация');

  const response = await fetch('/favorite/get', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('Ошибка получения избранного (статус):', response.status);
    console.error('Тело ошибки:', errorText.substring(0, 500));
    
    throw new Error(`Не удалось получить избранное: ${response.status}`);
  }

  const data = await response.json();
  return Array.isArray(data) ? data : (data.product || []);
};


//Список адресов
  const getAddress = async (user) => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('Требуется авторизация');

  const response = await fetch('/address/get/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  return await response.json();
};


// Создание адреса 
 const addAddress = async (info) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch('/address/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(info)
  });
  return await response.json();
};

//Редактирование адреса
const patchAddress = async (adrId,info) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch(`/address/update/${adrId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(info)
  });
  return await response.json();
};

// Удаление адреса
const deleteAddress = async (adrId) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch(`/address/delete/${adrId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },  
  });
  if (response.status === 204) {
    return {}; 
  }
  return await response.json();
};

//Создание отзыва
const addReview = async (prodId,info) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch(`/review/create/${prodId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(info)
  });
  return await response.json();
};

//Список отзывов о продукте
 const getReviewList = async (prodId) => {
    const response = await fetch(`/review/get/${prodId}`,
      {method:'GET',
          headers: {'Content-Type':'application/json',
          'accept':'application/json'},
        })
    console.log(response)
    const info = await response.json()
    console.log(info)
    return info
   }

//Добавить в корзину
const addBasket = async (prodId) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch('/cart/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ product_id: prodId})
  });
  return await response.json();
};


//Список корзины
const getBasket = async (user) => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('Требуется авторизация');

  const response = await fetch('/cart/get/cart', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.status === 404) {
    return [];
  }

  if (!response.ok) {
    const errorText = await response.text();
    console.error('Ошибка получения корзины (статус):', response.status);
    console.error('Тело ошибки:', errorText.substring(0, 500));
    throw new Error(`Не удалось получить корзину: ${response.status}`);
  }

  return await response.json();
};

// Удаление товара из корзины
const deleteBasket = async (prodId) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch(`/cart/delete/${prodId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },  
  });
  if (response.status === 204) {
    return {}; 
  }
  return await response.json();
};

//Список заказов
const getOrders = async (user) => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('Требуется авторизация');

  const response = await fetch(`/order/get_list_order`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  return await response.json();
};


//Детали заказа
const getOrderItems = async (user,orderId) => {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('Требуется авторизация');

  const response = await fetch(`/order/get_orderitems/${orderId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  return await response.json();
};

//Создание заказа
 const addOrders = async (info) => {
 const token = localStorage.getItem('access_token');
 const response = await fetch('/order/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(info)
  });
  return await response.json();
};


    const value = {
        user,
        login,
        logOut,
		loadingAuth,
        registrationUser,
        getCategory,
        getProduct,
        getProductDetail,
        getProfile,
        addFavorites,
        getFavorites,
        deleteFavorites,
        getAddress,
        addAddress,
        patchAddress,
        deleteAddress,
        addReview,
        getReviewList,
        addBasket,
        getBasket,
        deleteBasket,
        getOrders,
        addOrders,
        getOrderItems
        

    }

    return (
        <Auth.Provider value = {value} >
            {children}
        </Auth.Provider>
    )

    }





export function useAuth(){
    const context = useContext(Auth);
    if (!context){
        console.log('ошибка context')
        return
    }
    return context;
}


export {Auth};