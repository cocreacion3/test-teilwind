import React from 'react'
import iot from '../../svg/iot.svg'
import hgm from '../../svg/hgm.svg'

export default function Header() {
    return (
        <div className=" h-32 flex items-end justify-end px-32">
            <div className=" h-32 items-end grid grid-flow-row auto-rows-max justify-items-center py-1">
                <span className="text-white text-4xl font-bold mb-2">Plataforma</span>
                <div className="grid grid-cols-2 content-end py-2 ">
                <img src={hgm} alt="IoT" className="w-32 rounded-full ml-4" />
                <img src={iot} alt="IoT" className="w-32 rounded-full ml-4" />
                </div>
            </div>

        </div>
    );
}
