import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import Dashboard from '../Dashboard'
import Testbutton from './Testbutton'


import { TimelapseProvider } from '../providers/SidebarContext'
import { ShaftProvider } from '../providers/SidebarContext'
import { DataFilterProvider } from '../providers/SidebarContext'
import { DevServSelectedProvider} from '../providers/SidebarContext'



const queryClient = new QueryClient();

export default function Layout() {
  return (
    <div className="flex flex-row h-screen w-screen overflow-hidden px-5 py-5 bg-hero_pattern bg-no-repeat bg-cover">
      <QueryClientProvider client={queryClient}>
        <TimelapseProvider><ShaftProvider><DataFilterProvider><DevServSelectedProvider>
          <Sidebar />
          <Testbutton />
          </DevServSelectedProvider></DataFilterProvider></ShaftProvider></TimelapseProvider>

        {/* <DevServSelectedProvider>
          <Testbutton/>
        </DevServSelectedProvider> */}
      </QueryClientProvider>

      
      <div className='flex-1'>
        <Header />
        <Dashboard />
      </div>
    </div>
  );
}



