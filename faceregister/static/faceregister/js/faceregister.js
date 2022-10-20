//process facedetection
const modal = document.getElementById("myModal");
const btn = document.getElementById("myBtn");
const modalcontent = document.querySelector(".modal-content1");
const noti_percent = document.querySelector(".noti-percent");
const noti_alert = document.querySelector(".noti-alert");
let video;
let localstream;
//thông báo
function Alertgreen() {
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

function Alertred() {
  const alert = document.querySelector(".alert-red");
  const closebtn = document.querySelector(".close-btn-red");
  alert.classList.add("show");
  alert.classList.remove("hide");
  alert.classList.add("showAlert");
  alert.style.display = "block";
  setTimeout(function () {
    alert.classList.remove("show");
    alert.classList.add("hide");
    etTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  }, 1000);
  closebtn.onclick = () => {
    alert.classList.remove("show");
    alert.classList.add("hide");
    etTimeout(function () {
      alert.style.display = "none";
    }, 1000);
  };
}
// tạo video
function CreateVideo() {
  video = document.createElement("video");
  video.id = "video";
  // video.style.width = "100%";
  // video.style.height = "100%";
  video.setAttribute("autoplay", "autoplay");
  video.setAttribute("muted", "muted");
}
//api upload ảnh đăng ký
function ApiUpload(dataconvert, MaSV, video, localstream) {
  Alertgreen();
  close_modal(video, localstream);
  let data = JSON.stringify({ "duong_dan_anh": dataconvert, "masv": MaSV });
  const config = {
    method: "POST",
    url: "/faceregister/savefrontalface/",
    headers: {
      //   'Authorization': 'Token c148eaabe85be02995148063c5c3b61dd1558a63',
      "Content-Type": "application/json",
    },
    data: data,
  };
  axios(config)
    .then(function (response) {
      
      console.log(response.data);
    })
    .catch(function (error) {
      Alertred();
      close_modal(video, localstream);
      console.log(error);
    });
}

//đóng modal
function close_modal(video, localstream) {
  modal.style.display = "none";
  video.src = "";
  localstream.getTracks()[0].stop();
  console.log("Vid off");
  modalcontent.removeChild(video);
}
//load module
faceapi.nets.tinyFaceDetector.loadFromUri("/static/faceregister/js/models");
//mở modal
btn.onclick = function () {
      noti_percent.innerHTML = "Di chuyển mặt vào camera";
  const MaSV = document.querySelector("#MaSV").value;
  if (MaSV.length > 0) {
    modal.style.display = "block";
    CreateVideo();
    modalcontent.appendChild(video);

    if (navigator.mediaDevices.getUserMedia !== null) {
      var options = {
        video: true,
        audio: false,
      };
      navigator.webkitGetUserMedia(
        options,
        function (stream) {
          video.srcObject = stream;
          localstream = stream;
          console.log("streaming");
          //console.log(dataURL)
        },
        function (e) {
          console.log("background error : " + e.name);
        }
      );
    }
  } else alert("vui lòng nhập mã sinh viên");
  //cắt mặt
  async function extractface(video, dataconvert) {
    // console.log(dataconvert.length)
    let detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()
    );
    while (detections == undefined || detections.length != 1 ||detections[0]._score < 0.80) {
      console.log(detections.length);
      detections = await faceapi.detectAllFaces(
        video,
        new faceapi.TinyFaceDetectorOptions()
      )
    }
    const regionsToExtract = [
      new faceapi.Rect(
        detections[0].box.x,
        detections[0].box.y,
        detections[0].box.width,
        detections[0].box.width
      ),
    ];
    let faceImages = await faceapi.extractFaces(video, regionsToExtract);
    //convert to canvas size 120x120
    faceImages.forEach((cnv) => {
      let canvas = document.createElement("canvas");
      canvas.width = "140";
      canvas.height = "140";
      let ctx = canvas.getContext("2d");
      ctx.drawImage(cnv, 0, 0, canvas.width, canvas.height);
      dataconvert.push(
        canvas
          .toDataURL("image/jpeg", 1.0)
          .replace("data:image/jpeg;base64,", "")
      );
      noti_percent.innerHTML =
        "Đang lấy ảnh " + Math.floor((dataconvert.length / 20) * 100) + "%";
      console.log(dataconvert);
    });
    demo(video, dataconvert, MaSV, localstream);
  }
  //hàm main
  function demo(video, dataconvert, MaSV, localstream) {
    console.log(dataconvert.length);
    if (dataconvert.length < 20) {
      setTimeout(async () => {
        extractface(video, dataconvert);
      }, 100);
    } else {
      noti_percent.innerHTML = "Đang xử lý";
      console.log("push");
      ApiUpload(dataconvert, MaSV, video, localstream);
    }
  }
  // crop face image
  video.addEventListener("play", () => {
    let dataconvert = [];
    demo(video, dataconvert, MaSV, localstream);
  });
  // close modal khi kích nút x hoặc vùng trống
  let close = document.querySelector(".close");
  close.onclick = () => {
    close_modal(video, localstream);
  };
  window.onclick = function (event) {
    if (event.target == modal) {
      close_modal(video, localstream);
    }
  };
};
