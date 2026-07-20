
# 1. Fix app.py paths for 012 and 013
with open('modules/Dental_Panoramic_Reader/app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

app_content = app_content.replace('get_model_path("Dental_012/weights/best.onnx"', 'get_model_path("Dental_012/models/best.onnx"')
app_content = app_content.replace('get_model_path("Dental_013/weights/best.onnx"', 'get_model_path("Dental_013/models/best.onnx"')

with open('modules/Dental_Panoramic_Reader/app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# 2. Fix Dental_014 inference.py
inf_path = 'modules/Dental_014/src/dental_014/inference.py'
with open(inf_path, 'r', encoding='utf-8') as f:
    inf_content = f.read()

# Fix out_channels=3
inf_content = inf_content.replace('OsteoMAENet(in_channels=3, out_channels=3, num_classes=3)', 'OsteoMAENet(in_channels=3, num_classes=3)')

# Fix weights_only=True
inf_content = inf_content.replace('weights_only=True', 'weights_only=False')

with open(inf_path, 'w', encoding='utf-8') as f:
    f.write(inf_content)

print("All fixes applied!")
