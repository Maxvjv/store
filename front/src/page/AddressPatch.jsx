import { useState, useEffect } from 'react';
import { useNavigate,useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';

function AddressPatch() {
const { user, patchAddress } = useAuth();
const { adrId } = useParams();
const navigate = useNavigate();

const [country,setCountry] = useState('')
const [city,setCity] = useState('')
const [street,setStreet] = useState('')
const [house,setHouse] = useState('')
const [apartment,setApartment] = useState('')
const [postal_code,setPostalcode] = useState('')

const handleAddress = async (e) => {


   const data = {
    'country': country,
    'city':city,
    'street': street,
    'house':house,
    'apartment':apartment,
    'postal_code':postal_code,
  }
   await patchAddress(adrId,data)
   navigate('/address');
}
	return(
	<div>
	<h2>Редактирование Адреса</h2>
	<p>Страна</p>
    <input type='text' value = {country} onChange={(e)=>{setCountry(e.target.value)}}/><br/>
     <p>Город</p>
    <input type='text' value = {city} onChange={(e)=>{setCity(e.target.value)}}/><br/>
     <p>Улица</p>
    <input type='text' value = {street} onChange={(e)=>{setStreet(e.target.value)}}/><br/>
	<p>Дом</p>
    <input type='text' value = {house} onChange={(e)=>{setHouse(e.target.value)}}/><br/>
     <p>Апартаменты</p>
    <input type='text' value = {apartment} onChange={(e)=>{setApartment(e.target.value)}}/><br/>
     <p>Код</p>
    <input type='text' value = {postal_code} onChange={(e)=>{setPostalcode(e.target.value)}}/><br/>
	<button onClick={()=>{handleAddress()}}>Сохранить</button>
	</div>
	


	
	)
	
}


export default AddressPatch;