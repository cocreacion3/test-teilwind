import React, { createContext, useContext, useState } from 'react';
import { FcWorkflow } from 'react-icons/fc'
import { GoSun } from 'react-icons/go'
import { BsFillMoonStarsFill } from 'react-icons/bs'

import { useTimelapse } from '../providers/SidebarContext'
import { useShaft } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';

// import { udeGetList, QueryDevServResultContext } from '../providers/QuerysManager'
import { useGetList, QueryDevServResultContext } from '../providers/QuerysManager'


export default function Sidebar() {

    //////////////////////////////////////////////////////////////  Timelapse buttons
    const { timelapse, updateTimelapse } = useTimelapse();
    const handleClickPeriodicity = (name) => {
        updateTimelapse(name);
    }
    // console.log("timelapse en sidebar =", timelapse);
    //////////////////////////////////////////////////////////////  Shaft buttons
    const { shaft, updateShaft } = useShaft();
    const handleClickShaft = (name) => {
        updateShaft(name);
    }
    // console.log("shaft en sidebar =", shaft);
    //////////////////////////////////////////////////////////////  Services or Devices buttons
    const { dataFilter, updateDataFilter } = useDataFilter();
    const handleClickDataFilter = (name) => {
        updateDataFilter(name);
    }

    //////////////////////////////////////////////////////////////  Query list of Devices or Services
    const { isLoadingListItems, incomingDataListItems } = useGetList(dataFilter);
    const contextValue = useContext(QueryDevServResultContext);

    let devices = incomingDataListItems?.data || [];
    if (incomingDataListItems?.data && Array.isArray(incomingDataListItems.data)) {
        devices = incomingDataListItems.data;
    }

    //////////////////////////////////////////////////////////////  device or service selected from list of devices
    const { selectedDevServ, updateDevServSelected } = useDevServSelected();
    const handleClickServDevSelected = (name) =>{
        updateDevServSelected(name);
        // console.log("on sidebar", name);
    }

    ////////////////////////////////////////////////////////////// 


    return (
        <div className="flex flex-col p-10 w-60  text-white">
            <div className="flex items-center gap-1 py-1 rounded-xl text-center justify-center">

                <span className="text-neutral-100 text-4xl font-bold">MAGA</span>

            </div>

            <div className="items-center flex-1 py-5 flex flex-col gap-0.5">
                <span className="text-withe text-xl font-bold ">Fecha</span>
                <button className='commond-buttons'>D/M/A</button>
                <span className="text-withe text-xl font-bold ">Periodicidad</span>
                <ul className="text-center">
                    <li className={timelapse === 'daily' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('daily')}><button>Diario</button></li>
                    <li className={timelapse === 'weekly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('weekly')}><button>Semanal</button></li>
                    <li className={timelapse === 'monthly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('monthly')}><button>Mensual</button></li>
                    <li className={timelapse === 'yearly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('yearly')}><button>Anual</button></li>
                </ul>
                <span className="text-withe text-xl font-bold ">Turno</span>
                <ul className="grid grid-cols-2 gap-4 text-center">
                    <li className={shaft === 'day' ? "commond-buttons-active flex flex-col items-center justify-center" : 'commond-buttons flex flex-col items-center justify-center'} onClick={() => handleClickShaft('day')}>
                        <GoSun fontSize={30} />
                        <button>Día</button></li>
                    <li className={shaft === 'nigth' ? "commond-buttons-active flex flex-col items-center justify-center" : 'commond-buttons flex flex-col items-center justify-center'} onClick={() => handleClickShaft('nigth')}>
                        <BsFillMoonStarsFill fontSize={28} />
                        <button>Noche</button></li>
                </ul>
                <span className="text-withe text-xl font-bold ">Filtrar por</span>
                <ul className="text-center">
                    <li className={dataFilter === 'devices' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickDataFilter('devices')}><button>Dispositivo</button></li>
                    <li className={dataFilter === 'services' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickDataFilter('services')}><button>Servicio</button></li>

                </ul>


                <span className="text-withe text-xl font-bold ">Seleccionar</span>
                <div className="w-40 h-48 overflow-y-auto py-2">
                    {Array.isArray(devices) && devices.length > 0 && devices.map((device, index) => (
                        <label className="flex items-center mb-2" key={index}>
                            <input type="radio" name="selected-dev-serv" value={device} className="form-checkbox h-5 w-5 text-blue-600"  onClick={() => handleClickServDevSelected(device)}></input>
                            <span className="ml-2">{device}</span>
                        </label>
                    ))}


                </div>
            </div>
        </div>
    )
}
