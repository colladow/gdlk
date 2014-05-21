(function(window, angular) {

  var combos = angular.module('gdlk.combos');

  combos.factory('Combo', function($http, httpUtils) {

    return {
      query: function() {
        return httpUtils.checkStatusCode($http.get('combos/'));
      },

      get: function(id) {
        return httpUtils.checkStatusCode($http.get('combos/' + id));
      }
    };

  });

})(window, window.angular);
