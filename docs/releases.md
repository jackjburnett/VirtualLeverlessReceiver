---
layout: default
title: Releases
---

# Releases

<div id="releases-list"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
  $(document).ready(function() {
    $.getJSON('https://api.github.com/repos/jackjburnett/VirtualLeverlessReceiver/releases', function(data) {
      var releasesHtml = '<ul>';
      $.each(data, function(index, release) {
        releasesHtml += '<li><a href="' + release.html_url + '">' + release.name + '</a> - ' + release.published_at + '</li>';
      });
      releasesHtml += '</ul>';
      $('#releases-list').html(releasesHtml);
    });
  });
</script>