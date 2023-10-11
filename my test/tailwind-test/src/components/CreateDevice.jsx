import React, { useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';

import Header from './shared/Header'

export default function CreateDevice() {
    const [formData, setFormData] = useState({
        deviceId: '',
        service: '',
        area: '',
        cubicle: '',
    });

    const [responseData, setResponseData] = useState(null); // State to store the response data


    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData({
            ...formData,
            [id]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Construct the query
        const query = `http://127.0.0.1:3001/create_device?deviceId=${formData.deviceId}&service=${formData.service}&area=${formData.area}&cubicle=${formData.cubicle}&room=${formData.room}`;

        // Send the GET request using axios
        axios.get(query).then((response) => {
                // Handle the response data here
                console.log('Data received:', response.data);
                setResponseData(response.data);
                setTimeout(() => {setResponseData(null);}, 5000);
            })
            .catch((error) => {
                // Handle any errors
                console.error('Error:', error);
                setResponseData(null);
            });
    };
    return (
        <div className="flex-row h-screen w-screen overflow-hidden px-5 py-5 bg-hero_pattern bg-no-repeat bg-cover">
            <Header/>
        <form className="px-10 py-10" onSubmit={handleSubmit}>
            <div className="mb-6">
                <label htmlFor="deviceId" className="block mb-2 text-sm font-medium text-gray-100">
                    Id del dispositivo
                </label>
                <input
                    type="text"
                    id="deviceId"
                    className="w-64 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="MAGA-001"
                    required
                    value={formData.deviceId}
                    onChange={handleInputChange}
                />
            </div>
            <div className="mb-6">
                <label htmlFor="service" className="block mb-2 text-sm font-medium text-gray-100">
                    Nombre del servicio
                </label>
                <input
                    type="text"
                    id="service"
                    className="w-64 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="UCI"
                    required
                    value={formData.service}
                    onChange={handleInputChange}
                />
            </div>
            <div className="mb-6">
                <label htmlFor="area" className="block mb-2 text-sm font-medium text-gray-100">
                    Área de ubicación
                </label>
                <input
                    type="text"
                    id="area"
                    className="w-64 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Enfermeria"
                    required
                    value={formData.area}
                    onChange={handleInputChange}
                />
            </div>
            <div className="mb-6">
                <label htmlFor="cubicle" className="block mb-2 text-sm font-medium text-gray-100">
                    Cubículo
                </label>
                <input
                    type="text"
                    id="cubicle"
                    className="w-64 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="001"
                    required
                    value={formData.cubicle}
                    onChange={handleInputChange}
                />
            </div>
            <div className="mb-6">
                <label htmlFor="room" className="block mb-2 text-sm font-medium text-gray-100">
                    Habitación
                </label>
                <input
                    type="text"
                    id="room"
                    className="w-64 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="001"
                    required
                    value={formData.room}
                    onChange={handleInputChange}
                />
            </div>
            <div className="w-64 py-2">
                <p className="py-2 text-gray-200">
                    * Diligencie todos los campos. Si no es necesario uno de los datos, rellénelo con "None".
                </p>
            </div>
            <button type="submit" className="commond-buttons">
                Crear dispositivo
            </button>
            {responseData && (<div className="font-bold text-gray-100  w-64 text-center">
          <span >{responseData+'!!!'}</span>
        </div>
      )}
        </form>

    </div>
    );
}
