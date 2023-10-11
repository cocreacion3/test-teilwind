import React, { useState, useEffect } from 'react'
import Datepicker from "tailwind-datepicker-react"

import { useDate } from './providers/SidebarContext';

const options = {
    autoHide: true,
    todayBtn: false,
    clearBtn: true,
    maxDate: new Date("2030-01-01"),
    minDate: new Date("2023-01-01"),
    theme: {
      background: "bg-gray-100",
      todayBtn: "",
      clearBtn: "",
      icons: "",
      text: "",
      disabledText: "bg-gray-200",
      input: "text-xs font-blod",
      inputIcon: "",
      selected: "",
      defaultDate: new Date("2023-01-01"),
    },
    icons: {
      prev: () => <span>{'<'}</span>,
      next: () => <span>{'>'}</span>,
    },
    language: "es",
    datepickerClassNames: "top-12",
  };
  

  const DateSelector = () => {
    const { selectedDate, setDate } = useDate();
    const [show, setShow] = useState(false); // Define setShow as a state function
  
    const handleChange = (selectedDate) => {
      const day = selectedDate.getUTCDate();
      const month = selectedDate.getUTCMonth() + 1;
      const year = selectedDate.getUTCFullYear();
  
      setDate(day, month, year);
    };
  
    const handleClose = () => {
      setShow(false); // Update the show state to close the date picker
    };
  
    return (
      <div>
        <Datepicker options={options} onChange={handleChange} show={show} setShow={setShow} />
      </div>
    );
  };
  
  export default function Datesel() {
    return <DateSelector />;
  }