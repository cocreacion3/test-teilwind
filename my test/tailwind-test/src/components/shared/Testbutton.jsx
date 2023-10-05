import React, { useState, useEffect } from 'react'

import { useTimelapse } from '../providers/SidebarContext'
import { useShaft } from '../providers/SidebarContext'
import { useDataFilter } from '../providers/SidebarContext'
import { useDevServSelected } from '../providers/SidebarContext';

export default function Testbutton() {

    const { timelapse, updateTimelapse } = useTimelapse();
    const { shaft, updateShaft } = useShaft();
    const { dataFilter, updateDataFilter } = useDataFilter();
    const { devServSelected, updateDevServSelected } = useDevServSelected();
    
    console.log("timelapse:", timelapse, "shaft:", shaft, "type:", dataFilter, "selected:", devServSelected);


  return (
<div > klAJSEDGHRFKJIQWEHRFT</div>
  )
}
