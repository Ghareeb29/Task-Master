import React, {useState} from 'react';
import Cards from './cards';
import { FaPlus } from "react-icons/fa6";
import InputData from './InputData';

function Alltasks() {
    const [InputDiv, SetInputDiv] = useState("hidden");
    return (
        <>
            <div>
                <div className='w-full flex justify-end px-4 py-2'>
                    <button onClick={() => SetInputDiv("fixed")}>
                        <FaPlus className='text-4xl text-gray-300 hover:text-gray-100 transition-all duration-300'/>
                    </button>
                </div>
                <Cards home={"true"} SetInputDiv={SetInputDiv} />
            </div>
            <InputData InputDiv={InputDiv} SetInputDiv={SetInputDiv} />
        </>
        
    );
};

export default Alltasks;