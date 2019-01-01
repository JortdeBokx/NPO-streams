class BaseStreamHandler:

    def get_lineup(self):
        """
        Creates a lineup of available channels in a json object
        :return: Array of available channels in json format according to above structure
        """
        raise NotImplementedError("Please Implement this method")
