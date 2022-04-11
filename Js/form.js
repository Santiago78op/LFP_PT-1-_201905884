function GetById()
{
    var entrada= document.getElementsByName("entrada");
    var result='';
    for(var i=0; i<entrada.length; i++)
    {
    result=result+entrada[i].value +"<br/>";
    }

    document.getElementById("div1").innerHTML= result;


    var ele = document.getElementsByTagName('radios');
      
    for(i = 0; i < ele.length; i++) {
          
        if(ele[i].type="radio") {
          
            if(ele[i].checked)
                result=result+ele[i].name+" Value: "+ele[i].value+"<br>";

                        
        }
    }
    
    document.getElementById("div1").innerHTML= result;

    
    var my_data = document.getElementsByName('opciones'); 
    sel_index=my_data[0].selectedIndex
    sel_index=my_data[0].selectedIndex // Index number of Selection
    sel_value=my_data[0][sel_index].value 
    if(sel_index > 0){
        result=result+sel_value+"<br/>";
        }else{
            result=result+" No Selection"
        }

    

}


function Entrada() {
    var iframe=document.getElementById("myframe")
    iframe.src = "../../Data/form.txt";
}