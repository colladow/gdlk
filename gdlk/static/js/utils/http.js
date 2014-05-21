(function(window, angular) {
  'use strict';

  var utils = angular.module('gdlk.utils');

  utils.factory('httpUtils', function($q) {
    return {
      checkStatusCode: function(request, desiredCode) {
        var deferred = $q.defer();

        desiredCode = desiredCode || 200;

        request.then(function(response) {
          if (response.status === 200) {
            deferred.resolve(response.data);
          } else {
            deferred.resolve(response);
          }
        });

        return deferred.promise;
      }
    };
  });

})(window, window.angular);
