const signupBtn = document.querySelector('#signup')
const modal = document.getElementById("myModal");
const modalcontent = document.querySelector(".modal-content1");
const noti_percent = document.querySelector(".noti-percent");
const noti_alert = document.querySelector(".noti-alert");
console.log("hello");
//thông báo
function Alertgreen() {
  console.log("hell")
  const alert = document.querySelector(".alert-green");
  const closebtn = document.querySelector(".close-btn-green");
  alert.classList.add("show");
  alert.classList.remove("hide");
  alert.classList.add("showAlert");
  
  alert.style.display = "block";
  setTimeout(function () {
    alert.classList.remove("show");
    alert.classList.add("hide");
    setTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  }, 1000);
  closebtn.onclick = () => {
    alert.classList.remove("show");
    alert.classList.add("hide");
    setTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  };
}
async function callSignUpAPI(data){
  const config = {
      method: 'POST',
      url: '/faceregister/takingfrontalface/',
      headers: { 
      //   'Authorization': 'Token c148eaabe85be02995148063c5c3b61dd1558a63', 
        'Content-Type': 'application/json'
      },
      data : data
    };
    
  axios(config)
  .then(function (response) {
    console.log(JSON.stringify(response.data));
    Alertgreen();
  })
  .catch(function (error) {
    console.log(error);
    console.log(error.response);
    console.log(error.response.data);
    // for (const key in error.response.data){
    //   console.log(`${key}: ${error.response.data[key]}`);
    //   const noti = document.createElement("p")
    //   noti.innerHTML = `${key}: ${error.response.data[key]}`  
    //   notification.appendChild(noti);
    //   notification.appendChild(document.createElement("br"))
    // }
    // for(let i = 0; i<error.response.data.length; i++){
    //   notification.appendChild(document.createElement("p").innerHTML 
    //                             = error.response.data[i])
    // }
  });
}

signupBtn.onclick = () => {
    const fullName = document.querySelector('#fullname').value
    const phoneNumber = document.querySelector('#phone-number').value
    const studentCode = document.querySelector('#student-code').value
    const birthday = document.querySelector('#birthday').value
    const maleGender = document.querySelector('#male')
    console.log("click")
    const data = JSON.stringify({
        "masv": studentCode,
        "ho_ten": fullName,
        "nam_sinh": birthday,
        "so_dien_thoai": phoneNumber,
        "gioi_tinh": maleGender.checked
    });
    
      callSignUpAPI(data)
      
}


