import React from 'react'
import iot from '../../svg/iot.svg'
import hgm from '../../svg/hgm.svg'
import { Link } from "react-router-dom";

export default function Header() {
    return (
        <div className=" h-32 flex items-end justify-end px-32 py-4">
            <div className=" h-32 items-end grid grid-flow-row auto-rows-max justify-items-center py-1">
                <Link to="/projects">
                <span className="text-white text-4xl font-bold mb-2">Plataforma</span>
                <div className="grid grid-cols-2 content-end py-2 ">
                <img src={hgm} alt="IoT" className="w-32 ml-4" />
                <img src={iot} alt="IoT" className="w-32 ml-4" />
                </div>
                </Link>
            </div>

        </div>
    );
}
