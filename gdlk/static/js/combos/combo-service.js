(function(window, angular) {

  var combos = angular.module('gdlk.combos');

  combos.factory('Combo', function($http) {

    return {
      query: function() {
        return $http.get('combos/');
      }
    };

    // return $resource('combos/:comboID', {}, {
    //   query: {
    //     method: 'GET',
    //     params: {
    //     },
    //     isArray: true
    //   }
    // });

  });

})(window, window.angular);
