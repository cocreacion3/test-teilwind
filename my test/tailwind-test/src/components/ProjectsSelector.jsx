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
                <div className='grid grid-rows-2 grid-flow-col gap-24 h- justify-center text-white'>
                    <Link to="/maga" className='text-white'>
                        <div className='flex flex-col items-center text-center'>
                            <BiMeteor fontSize={150} className='hover:animate-ping' />
                            <div className='font-bold text-4xl no-underline'>MAGA</div>
                        </div>
                    </Link>

                    <div className='flex flex-col items-center text-center text-gray-400'>
                        <BiMeteor fontSize={150} />
                        <div className='font-bold text-4xl '>Proyecto x</div>
                    </div>

                    <div className='flex flex-col items-center text-center text-gray-400'>
                        <BiMeteor fontSize={150} />
                        <div className='font-bold text-4xl'>Sonómetro</div>
                    </div>

                    <div className='flex flex-col items-center text-center text-gray-400'>
                        <BiMeteor fontSize={150} />
                        <div className='font-bold text-4xl'>Proyecto y</div>
                    </div>

                    <div className='flex flex-col items-center text-center text-gray-400'>
                        <BiMeteor fontSize={150} />
                        <div className='font-bold text-4xl'>Proyecto z</div>
                    </div>

                    <div className='flex flex-col items-center text-center text-gray-400'>
                        <BiMeteor fontSize={150} />
                        <div className='font-bold text-4xl'>Proyecto w</div>
                    </div>
                </div>
                <Footer />
            </div>
        </div>
    )
}
