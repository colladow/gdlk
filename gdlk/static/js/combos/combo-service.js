(function(window, angular) {

  var combos = angular.module('gdlk.combos');

  combos.factory('Combo', function($http, serviceUtils) {

    return {
      query: function() {
        return serviceUtils.checkStatusCode($http.get('combos/'));
      },

      get: function(id) {
        return serviceUtils.checkStatusCode($http.get('combos/' + id));
      }
    };

  });

})(window, window.angular);
