$(document).ready(function () {
    $('#a-take-photo').click(function (ev) {
        ev.preventDefault();

        const player = document.getElementById('player');
        const canvas = document.getElementById('img-canvas');
        const context = canvas.getContext('2d');
        const captureButton = document.getElementById('btn-capture');
        const constraints = {
            video: true
        };

        $('#video-area').show();

        captureButton.addEventListener('click', () => {
            context.drawImage(player, 0, 0, canvas.width, canvas.height);
            $('#form-base64').show();
        });

        $('#form-base64').submit(function () {
            player.srcObject.getVideoTracks().forEach(track => track.stop());
            var dataURL = canvas.toDataURL();
            $('#img-base64').val(dataURL);
            console.log(dataURL);
        });

        navigator.mediaDevices.getUserMedia(constraints)
            .then((stream) => {
                player.srcObject = stream;
            });

    });
});