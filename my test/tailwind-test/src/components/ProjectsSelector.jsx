import React from 'react'
import Header from './shared/Header'
import Dashboard from './Dashboard'
import Footer from './shared/Footer'
import { BiMeteor } from 'react-icons/bi'
import { Link } from "react-router-dom";

export default function ProjectsSelector() {
    return (
        <div className="flex flex-row h-screen w-screen overflow-hidden px-5 py-5 bg-hero_pattern bg-no-repeat bg-cover">
            <div className='flex-1'>
                <Header />
                <div className=' h-fit py-10'>

                    <strong className='text-white px-5 text-7xl flex-1'>
                        ¡Bienvenido!
                    </strong>
                </div>
                <div className='py-2 grid grid-rows-2 grid-flow-col gap-32 h- justify-center text-white'>

                    <Link to="/" className='text-white'>
                        <div className='text-center font-bold text-4xl no-underline'><BiMeteor fontSize={150}  className='hover:animate-ping'/> MAGA</div>
                    </Link>
                    <div className='text-center font-bold text-4xl'><BiMeteor fontSize={150} /> MAGA</div>
                    <div className='text-center font-bold text-4xl'><BiMeteor fontSize={150} /> MAGA</div>
                    <div className='text-center font-bold text-4xl'><BiMeteor fontSize={150} /> MAGA</div>
                    <div className='text-center font-bold text-4xl'><BiMeteor fontSize={150} /> MAGA</div>
                    <div className='text-center font-bold text-4xl'><BiMeteor fontSize={150} /> MAGA</div>

                </div>
                <Footer />
            </div>
        </div>
    )
}
