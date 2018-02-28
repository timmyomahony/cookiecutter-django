'use strict';

/* global $ */

let APP = {
  components: {}, 
  utils: {
    getArgs: function($el) {
      try {
        return eval("(" + $el.attr("data-component-options") + ")") || {};
      } catch(ex) {
        return {};
      }
    }
  }
};

let bindComponents = function() {
    $("[data-component]").each(function() {
        let $el = $(this);
        let names = $el.attr('data-component').split(',');
        names.forEach((name) => {
          if (! (name in APP.components)) {
            console.error(`Component "${name}" is not defined`);
            return false;
          } else {
            let existing = $el.data('data-loaded-components');
            if (!existing) {
              existing = [];
              $el.data('data-loaded-components', existing);
            }
            if (! (name in $el.data('data-loaded-components'))) {
                let options = APP.utils.getArgs($el);
                let Constructor = APP.components[name];
                let obj = new Constructor($el, options);
                existing.push(name);
                $el.data('data-component', obj);
                console.log(`Component "${name}" loaded.`);
            } else {
                console.log(`Component "${name}" already loaded`);
            }
          }  
        });      
    });
};

APP.components.example = function($el, options) {
  let settings = $.extend({}, {}, options);
  let api = {};
  return api;
};

(function() {
  bindComponents();
})();