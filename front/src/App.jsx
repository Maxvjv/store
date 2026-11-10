import { useState, useEffect } from 'react'
import {BrowserRouter,Route,Routes} from 'react-router-dom'
import {AuthProvider} from './context/Auth';


import Header from './components/Header';


import Home from './page/Home';
import Login from './page/Login';
import Catalog from './page/Catalog';
import ProductList from './page/ProductList';
import ProductDetail from './page/ProductDetail';
import Profile from './page/Profile'
import Favorites from './page/Favorites'
import Address from './page/Address'
import AddressPatch from './page/AddressPatch'
import AddressCreate from './page/AddressCreate'
import Registration from './page/Registration';
import Review from './page/Review';
import ReviewList from './page/ReviewList';
import Basket from './page/Basket';
import Orders from './page/Orders';
import OrdersCreate from './page/OrdersCreate';
import OrderItems from './page/OrderItems';


function App() {


return (
  <AuthProvider>
    <BrowserRouter>
    <Header/>
    <Routes>

      <Route path='/' element={<Home/>}/> 
      <Route path='/catalog' element={<Catalog/>}/>
      <Route path="/catalog/:catId" element={<ProductList/>} />
      <Route path='/login' element={<Login/>}/>
      <Route path='/profile' element={<Profile/>}/>
      <Route path="/catalog/:catId/:prodId" element={<ProductDetail/>} />
      <Route path="/favorites/" element={<Favorites/>} />
      <Route path="/address" element={<Address/>} />
      <Route path="/address/update/:adrId" element={<AddressPatch/>} />
      <Route path="/address/addresscreate" element={<AddressCreate/>} />
      <Route path='/registration' element={<Registration/>}/>
      <Route path='/review/:prodId' element={<Review/>}/>
      <Route path='/reviewlist/:prodId' element={<ReviewList/>}/>
      <Route path='/basket' element={<Basket/>}/>
      <Route path='/myorders' element={<Orders/>}/>
      <Route path='/basket/orderscreate' element={<OrdersCreate/>}/>
      <Route path='/myorders/:orderId' element={<OrderItems/>}/>
    </Routes>
    </BrowserRouter>
    </AuthProvider>
  )

}

export default App