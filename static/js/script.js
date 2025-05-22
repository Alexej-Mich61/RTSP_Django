//static/js/script.js
$(document).ready(function() {
    console.log('script.js loaded');

    function setupHlsPlayer(videoElement, hlsUrl) {
        console.log(`Setting up HLS for camera ${videoElement.dataset.cameraId} with URL: ${hlsUrl}`);
        if (Hls.isSupported()) {
            const hls = new Hls({
                enableWorker: true,
                lowLatencyMode: true,
                backBufferLength: 90,
                maxBufferLength: 30,
                maxMaxBufferLength: 60,
                maxBufferSize: 60 * 1000 * 1000,
                maxFragLookUpTolerance: 0.2,
                liveSyncDurationCount: 3,
                liveMaxLatencyDurationCount: 10,
                debug: true
            });

            hls.loadSource(hlsUrl);
            hls.attachMedia(videoElement);

            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                console.log('HLS manifest parsed, playing video');
                videoElement.play().catch(function(error) {
                    console.error('Play error:', error);
                });
            });

            hls.on(Hls.Events.ERROR, function(event, data) {
                console.error('HLS error:', data);
                if (data.fatal) {
                    switch(data.type) {
                        case Hls.ErrorTypes.NETWORK_ERROR:
                            console.error('Fatal network error, attempting to recover...');
                            hls.startLoad();
                            break;
                        case Hls.ErrorTypes.MEDIA_ERROR:
                            console.error('Fatal media error, attempting to recover...');
                            hls.recoverMediaError();
                            break;
                        default:
                            console.error('Unrecoverable error, destroying HLS instance');
                            hls.destroy();
                            videoElement.poster = '/static/images/no-stream.jpg';
                            break;
                    }
                }
            });
        } else if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
            videoElement.src = hlsUrl;
            videoElement.addEventListener('loadedmetadata', function() {
                videoElement.play().catch(function(error) {
                    console.error('Play error:', error);
                });
            });
        } else {
            console.error('HLS not supported and native HLS playback not available');
            videoElement.poster = '/static/images/no-stream.jpg';
        }
    }

    $('.video-player').each(function() {
        const videoElement = this;
        const hlsUrl = videoElement.dataset.hlsUrl;
        setupHlsPlayer(videoElement, hlsUrl);
    });

    $(document).on('click', '.fullscreen-btn', function(e) {
        e.preventDefault();
        const cameraId = $(this).data('camera-id');
        const hlsUrl = $(`.video-player[data-camera-id="${cameraId}"]`).data('hls-url');
        const modalVideo = $('#fullscreenModal').find('video')[0];
        modalVideo.dataset.cameraId = cameraId;
        setupHlsPlayer(modalVideo, hlsUrl);
        $('#fullscreenModal').modal('show');
    });

    $('#fullscreenModal').on('hidden.bs.modal', function() {
        const modalVideo = $(this).find('video')[0];
        modalVideo.pause();
        modalVideo.src = '';
    });
});

$(document).on('click', '.video-player', function() {
    if (this.paused) {
        this.play().catch(function(error) {
            console.error('Play error:', error);
        });
    } else {
        this.pause();
    }
});