import React, { createContext, useContext, useState } from 'react';
import { FcWorkflow } from 'react-icons/fc'
import { GoSun } from 'react-icons/go'
import { BsFillMoonStarsFill } from 'react-icons/bs'

import { useTimelapse } from '../providers/SidebarContext'
import { useShift } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';
import { usePackagedData } from '../providers/SidebarContext';
import { useExportData } from '../providers/SidebarContext';

import Dateselector from '../Dateselector'


import { useGetList, QueryDevServResultContext } from '../providers/QuerysManager'


export default function Sidebar() {

    //////////////////////////////////////////////////////////////  Timelapse buttons
    const { timelapse, updateTimelapse } = useTimelapse();
    const handleClickPeriodicity = (name) => {
        updateTimelapse(name);
    }
    // console.log("timelapse en sidebar =", timelapse);
    //////////////////////////////////////////////////////////////  Shift buttons
    const { shift, updateShift } = useShift();
    const handleClickShift = (name) => {
        updateShift(name);
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
    const [selectedDeviceOrService, setSelectedDeviceOrService] = useState(null);
    const { selectedDevServ, updateDevServSelected } = useDevServSelected();
    const handleClickServDevSelected = (name) =>{
        updateDevServSelected(name);
        // console.log("on sidebar", name);
    }
    //////////////////////////////////////////////////////////////Export data
    const {packagedData, updatePackagedData} = usePackagedData();
    const { exportToCSV, exportedData } = useExportData();
    const handleExport = () => {
        if (packagedData.length > 0) {
            exportToCSV(packagedData, 'all_graphs_data.csv');
        }
      };

    return (
        <div className="flex flex-col p-10 w-60  text-white">
            <div className="flex items-center gap-1 py-1 rounded-xl text-center justify-center">

                <span className="text-neutral-100 text-4xl font-bold">MAGA</span>

            </div>

            <div className="items-center flex-1 py-5 flex flex-col gap-0.5">
                <span className="text-withe text-xl font-bold ">Fecha</span>
                {/* <button className='commond-buttons'>D/M/A</button> */}
                <Dateselector/>
                <span className="text-withe text-xl font-bold ">Periodicidad</span>
                <ul className="text-center">
                    <li className={timelapse === 'daily' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('daily')}><button>Diario</button></li>
                    <li className={timelapse === 'weekly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('weekly')}><button>Semanal</button></li>
                    <li className={timelapse === 'monthly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('monthly')}><button>Mensual</button></li>
                    <li className={timelapse === 'yearly' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => handleClickPeriodicity('yearly')}><button>Anual</button></li>
                </ul>
                <span className="text-withe text-xl font-bold ">Turno</span>
                <ul className="grid grid-cols-2 gap-4 text-center">
                    <li className={shift === 'day' ? "commond-buttons-active flex flex-col items-center justify-center" : 'commond-buttons flex flex-col items-center justify-center'} onClick={() => handleClickShift('day')}>
                        <GoSun fontSize={30} />
                        <button>Día</button></li>
                    <li className={shift === 'nigth' ? "commond-buttons-active flex flex-col items-center justify-center" : 'commond-buttons flex flex-col items-center justify-center'} onClick={() => handleClickShift('nigth')}>
                        <BsFillMoonStarsFill fontSize={28} />
                        <button>Noche</button></li>
                </ul>
                <span className="text-withe text-xl font-bold ">Filtrar por</span>
                <ul className="text-center">
                <li className={dataFilter === 'devices' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => { handleClickDataFilter('devices'); setSelectedDeviceOrService(null); handleClickServDevSelected(null); }}><button>Dispositivo</button></li>
                <li className={dataFilter === 'services' ? "commond-buttons-active" : 'commond-buttons'} onClick={() => { handleClickDataFilter('services'); setSelectedDeviceOrService(null);handleClickServDevSelected(null); }}><button>Servicio</button></li>
                </ul>


                <span className="text-withe text-xl font-bold ">Seleccionar</span>
                <div className="w-40 h-36 overflow-y-auto py-2 px-2">
                    {Array.isArray(devices) && devices.length > 0 && devices.map((device, index) => (
                        <label className="flex items-center mb-2" key={index}>
                            <input
                            type="radio"
                            name="selected-dev-serv"
                            className="form-checkbox h-5 w-5 text-blue-600"
                            onClick={() => {
                                handleClickServDevSelected(device);
                                setSelectedDeviceOrService(device); // Update the selected device or service
                            }}
                            checked={device === selectedDeviceOrService} // Set checked based on selected state
                        ></input>
                        <span className="ml-2">{device}</span>
                        </label>
                    ))}
                </div>
                <div className='py-3'>
                    <button className='commond-buttons py-10' onClick={handleExport}>Exportar</button>
                </div>
            </div>
        </div>
    )
}





