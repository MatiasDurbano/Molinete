import json

class JsonTraductor:

    def convertMensajeTarjeta(msgjson):
        ret = json.loads(msgjson)
        return ret["tarjetaId"]

    def convertValidaTarjeta(msg):
        ret = {"tarjeta_valida":msg}
        return json.dumps(ret)


    def convertEstadoSensor(msgjson):
        ret = json.loads(msgjson)
        return ret["sensor"]

    def convertMensajeHabilitado(msgjson):
        ret = json.loads(msgjson)
        return ret["habilitar"]

    def convertRespuestaServer(estado):
        ret = {"habilitar":estado}
        return json.dumps(ret)
