import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import Dashboard from '../Dashboard'


export default function Layout() {
  return (
    
        <div className="flex flex-row h-screen w-screen overflow-hidden px-5 py-5 bg-hero_pattern bg-no-repeat bg-cover">
        <Sidebar/>
        <div className='flex-1'>
          <Header/>
          {/* <div className="p-4">{<Outlet/>}</div> */}
          <Dashboard/>
          {/* <LineChart/> */}
        </div>
    </div>
  )
}
