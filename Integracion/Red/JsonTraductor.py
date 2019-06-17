import json

class JsonTraductor:

    def convertJsonTarjeta(id):
        ret = {"tarjetaId":id}
        return json.dumps(ret)

    def convertRespuestaTarjeta(msgjson):
        ret = json.loads(msgjson)
        return ret["tarjeta_valida"]

    def convertJsonSensor(estado):
        ret = {"sensor":estado}
        return json.dumps(ret)

    def convertMensajeServer(msgjson):
        ret = json.loads(msgjson)
        if 'habilitar' in ret:
            return ret["habilitar"]
        else:
            pass

    def convertRespuestaServer(estado):
        ret = {"habilitar":estado}
        return json.dumps(ret)
