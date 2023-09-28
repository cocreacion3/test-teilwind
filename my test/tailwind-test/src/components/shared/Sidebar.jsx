import React from 'react'
import {FcWorkflow} from 'react-icons/fc'
import {GoSun} from 'react-icons/go'
import {BsFillMoonStarsFill} from 'react-icons/bs'

export default function Sidebar() {
  return (
    <div className="flex flex-col p-10 w-60  text-white">
        <div className="flex items-center gap-1 py-1 rounded-xl text-center justify-center">

            <span className="text-neutral-100 text-4xl font-bold">MAGA</span>

        </div>

        <div className="items-center flex-1 py-5 flex flex-col gap-0.5">
            <span className="text-withe text-xl font-bold ">Fecha</span>
            <button className='commond-buttons'>D/M/A</button>
            <span className="text-withe text-xl font-bold ">Periodicidad</span>
                <ul className = "text-center">
                    <li className="commond-buttons"><button>Diario</button></li>
                    <li className="commond-buttons"><button>Semanal</button></li>
                    <li className="commond-buttons"><button>Mensual</button></li>
                    <li className="commond-buttons"><button>Anual</button></li>
                </ul>
            <span className="text-withe text-xl font-bold ">Turno</span>
                <ul className = "grid grid-cols-2 gap-4 text-center">
                    <li className="w-1 h-20 bg-white hover:bg-gray-100 text-blue-800 text-base font-bold py-1 px-10 border
                                border-gray-400 rounded-xl shadow mb-2 flex flex-col items-center justify-center">
                        <GoSun fontSize={30}/>
                        <button>Día</button></li>
                        <li className="w-1 h-20 bg-white hover:bg-gray-100 text-blue-800 text-base font-bold py-1 px-10 border
                                border-gray-400 rounded-xl shadow mb-2 flex flex-col items-center justify-center">
                        <BsFillMoonStarsFill fontSize={28}/>
                        <button>Noche</button></li>
                </ul>
            <span className="text-withe text-xl font-bold ">Filtrar por</span>
                <ul className = "text-center">
                    <li className="commond-buttons"><button>Dispositivo</button></li>
                    <li className="commond-buttons"><button>Servicio</button></li>

                </ul>


            <span className="text-withe text-xl font-bold ">Seleccionar</span>
            <div class="w-40 h-48  overflow-y-auto py-2">
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 001</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 002</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 003</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 004</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 005</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 006</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 007</span>
                </label>
                <label class="flex items-center mb-2">
                    <input type="radio" name="device" class="form-checkbox h-5 w-5 text-blue-600"></input>
                    <span class="ml-2">MAGA 008</span>
                </label>
                </div>
            </div>
        {/* <div>bottom part</div> */}
    </div>
  )
}
