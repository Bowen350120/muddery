
/*
 * callback_success: function(data)
 * callback_error: function(code, message)
 */
service = {
    sendQuery: function(path, func_no, args, callback_success, callback_error) {
	    var url = CONFIG.api_url + path;
	    params = {
            func: func_no,
            args: args,
        };

	    $.ajax({
            url: url,
		    type: "POST",
            contentType: "application/json",
		    cache: false,
		    data: JSON.stringify(params),
		    dataType: "json",
		    success: function(data) {
                if (!data) {
		            data = {
                        code: -1,
                        result: "Empty result.",
                    };
	            }
	            else if (!("code" in data) || !("result" in data)) {
                    data = {
                        code: -1,
                        result: "Wrong format.",
                    };
	            }
	            
                if (data.code != 0) {
		            console.log("Return error: " + data.code + "：" + data.result);
		            if (callback_error) {
			            callback_error(data.code, data.result);
		            }
	            }
	            else {
		            if (callback_success) {
			            callback_success(data.result);
		            }
	            }
            },
		    error: callback_error,
	    });
    },

    login: function(username, password, callback_success, callback_error) {
        var args = {
            username: username,
            password: password,
        };
        this.sendQuery("login", "", args, callback_success, callback_error);
    },

    logout: function(callback_success, callback_error) {
        this.sendQuery("logout", "", {}, callback_success, callback_error);
    },

    queryColumns: function(table_name, callback_success, callback_error) {
        var args = {
            table: table_name,
        };
        this.sendQuery("query_columns", "", args, callback_success, callback_error);
    },

    queryTable: function(table_name, callback_success, callback_error) {
        var args = {
            table: table_name,
        };
        this.sendQuery("query_table", "", args, callback_success, callback_error);
    },
}


