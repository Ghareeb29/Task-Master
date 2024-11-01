import React, {useState} from 'react';
import Cards from './cards';
import InputData from './InputData';

function Alltasks() {
    const [InputDiv, SetInputDiv] = useState("hidden");
    return (
        <>
            <div>
                <Cards home={"true"} SetInputDiv={SetInputDiv} /> 
            </div>
            <InputData InputDiv={InputDiv} SetInputDiv={SetInputDiv} />
        </>
        
    );
};

export default Alltasks;