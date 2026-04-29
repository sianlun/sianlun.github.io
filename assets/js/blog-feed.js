// ================================================================
// BLOG-FEED.JS — Fetch latest posts from WordPress.com REST API
// ================================================================
(function () {
  var container = document.getElementById('blog-posts');
  if (!container) return;

  var API_URL = 'https://public-api.wordpress.com/rest/v1.1/sites/sianlun.wordpress.com/posts/?number=4&fields=title,URL,date,excerpt';

  fetch(API_URL)
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (!data.posts || !data.posts.length) {
        container.innerHTML = '<p style="grid-column:1/-1;text-align:center;color:var(--text-muted);">No posts found.</p>';
        return;
      }

      container.innerHTML = '';

      data.posts.forEach(function (post) {
        var date = new Date(post.date);
        var monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        var dateStr = monthNames[date.getMonth()] + ' ' + date.getFullYear();

        // Strip HTML tags from excerpt and trim
        var tmp = document.createElement('div');
        tmp.innerHTML = post.excerpt || '';
        var excerpt = tmp.textContent || tmp.innerText || '';
        excerpt = excerpt.trim();
        if (excerpt.length > 160) {
          excerpt = excerpt.substring(0, 157) + '...';
        }

        var card = document.createElement('a');
        card.href = post.URL;
        card.target = '_blank';
        card.rel = 'noopener';
        card.className = 'blog-card';
        card.setAttribute('data-animate', '');

        card.innerHTML =
          '<div class="blog-date">' + dateStr + '</div>' +
          '<h4>' + post.title + '</h4>' +
          '<p>' + excerpt + '</p>' +
          '<span class="blog-read">Read more <i class="fa-solid fa-arrow-right"></i></span>';

        container.appendChild(card);
      });

      // Trigger scroll animations on newly added cards
      if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add('visible');
              observer.unobserve(entry.target);
            }
          });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        container.querySelectorAll('[data-animate]').forEach(function (el, i) {
          el.style.transitionDelay = (i % 4) * 0.08 + 's';
          observer.observe(el);
        });
      }
    })
    .catch(function () {
      // Fallback: show static links if API fails
      container.innerHTML =
        '<a href="https://sianlun.wordpress.com/recent-updates/" target="_blank" rel="noopener" class="blog-card visible">' +
          '<h4>Visit the Blog</h4>' +
          '<p>Read the latest posts at sianlun.wordpress.com</p>' +
          '<span class="blog-read">Go to blog <i class="fa-solid fa-arrow-right"></i></span>' +
        '</a>';
    });
})();
