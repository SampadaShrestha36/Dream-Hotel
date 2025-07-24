let tabcontents=document.getElementsByClassName('tab-content')
let tablinks=document.getElementsByClassName('tab-links')
function openLink(arg){
    for(let tabcontent of tabcontents)
    {
        tabcontent.classList.remove("active-tab")
    }
    for(let tablink of tablinks)
    {
        tablink.classList.remove("active")
    }
    document.getElementById(arg).classList.add("active-tab")
    event.currentTarget.classList.add("active")
}
// let tabcontentss=document.getElementsByClassName('tab-content')
// let tablinkss=document.getElementsByClassName('tab-links')
// function openLink(arg){
//     for(let tabcontent of tabcontentss)
//     {
//         tabcontent.classList.remove("active-tab")
//     }
//     for(let tablink of tablinkss)
//     {
//         tablink.classList.remove("active")
//     }
//     document.getElementById(arg).classList.add("active-tab")
//     event.currentTarget.classList.add("active")
// }



