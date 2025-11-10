(function(){
  function onReady(fn){
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  function attachValidation(root){
    // Target file inputs inside the TurfImage inline (StackedInline renders with id starting with turfimage_set or similar)
    var inputs = (root || document).querySelectorAll('input[type="file"][name$="-image"], input[type="file"][name="image"], input[type="file"][id$="id_image"]');
    inputs.forEach(function(input){
      if (input.__sizeValidatorAttached) return;
      input.__sizeValidatorAttached = true;
      input.addEventListener('change', function(e){
        var files = e.target.files || [];
        if (!files.length) return;
        var file = files[0];
        var maxBytes = 2 * 1024 * 1024; // 2MB
        if (file.size > maxBytes){
          // Try to display an inline error near the input
          var msg = 'Image is larger than 2MB. Please choose a smaller file.';
          try {
            // Clear the selection
            e.target.value = '';
          } catch (_) {}
          // Find or create a help/error element
          var container = e.target.closest('.form-row, .inline-related, .field');
          if (container){
            var existing = container.querySelector('.ts-file-size-error');
            if (!existing){
              existing = document.createElement('p');
              existing.className = 'ts-file-size-error';
              existing.style.color = '#ff6b6b';
              existing.style.marginTop = '4px';
              container.appendChild(existing);
            }
            existing.textContent = msg;
          } else {
            alert(msg);
          }
        } else {
          // Clear any previous error message when valid
          var c = e.target.closest('.form-row, .inline-related, .field');
          if (c){
            var err = c.querySelector('.ts-file-size-error');
            if (err) err.remove();
          }
        }
      });
    });
  }

  onReady(function(){
    attachValidation(document);

    // Support dynamically added inlines (Add another ...)
    document.body.addEventListener('click', function(ev){
      var t = ev.target;
      if (!t) return;
      // Works for both "Add another" button and Django's add-row links
      if (t.matches('.add-row a, .add-row, a.add-another, .grp-add-handler, .dynamic-btn-add')){
        setTimeout(function(){ attachValidation(document); }, 50);
      }
    }, true);

    // Also observe DOM changes to catch newly inserted inline rows
    var obs = new MutationObserver(function(muts){
      muts.forEach(function(m){
        if (m.addedNodes && m.addedNodes.length){
          m.addedNodes.forEach(function(node){
            if (node.nodeType === 1){
              attachValidation(node);
            }
          });
        }
      });
    });
    try {
      obs.observe(document.body, {childList: true, subtree: true});
    } catch (_) {}
  });
})();
