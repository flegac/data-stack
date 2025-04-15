import faust

# Définir l'application Faust
app = faust.App('kafka_stream_pipeline', broker='kafka://localhost:9092')


# Définir un modèle pour les messages
class Measure(faust.Record):
    datetime: str
    value: float
    sensor_id: str


# Définir des topics pour les mesures
input_topic = app.topic('input_measures', value_type=Measure)
intermediate_topic = app.topic('intermediate_measures', value_type=Measure)
output_topic = app.topic('output_measures', value_type=Measure)


# Étape 1: Agent pour lire les messages d'entrée et effectuer une première transformation
@app.agent(input_topic)
async def filter_negative_values(measures):
    async for measure in measures:
        if measure.value >= 0:
            print(f"Filtered measure: {measure}")
            await intermediate_topic.send(value=measure)


# Étape 2: Agent pour lire les messages intermédiaires et effectuer une deuxième transformation
@app.agent(intermediate_topic)
async def calculate_moving_average(measures):
    window_size = 5
    window = []
    async for measure in measures:
        window.append(measure.value)
        if len(window) > window_size:
            window.pop(0)
        if len(window) == window_size:
            moving_avg = sum(window) / window_size
            measure.value = moving_avg
            print(f"Calculated moving average: {measure}")
            await output_topic.send(value=measure)


# Étape 3: Agent pour lire les messages de sortie et effectuer une action finale (par exemple, imprimer)
@app.agent(output_topic)
async def print_final_results(measures):
    async for measure in measures:
        print(f"Final result: {measure}")


if __name__ == '__main__':
    app.main()
