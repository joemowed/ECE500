using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class bar_ui : MonoBehaviour
{
    public TMP_Text bar_text;
    public Image foreground_img;
    //  [SerializeField, Range(0f, 1f)]
    private float value = 0.5f;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        if (bar_text == null)
        {
            Debug.LogError("No in-bar text element defined for bar UI element", this);
        }
    }

    // Update is called once per frame
    void Update()
    {
        update_bar_fill();
        update_bar_text();
    }
    public void set_value(float new_value)
    {
        if (new_value < 0 || new_value > 1)
        {
            Debug.LogError($"Attempt to set bar value out of range. Value: {new_value} (allowed range 0-1)", this);
            new_value = Mathf.Clamp(new_value, 0, 1);
        }
        value = new_value;
    }
    private void update_bar_fill()
    {
        foreground_img.fillAmount = value;
    }
    private void update_bar_text()
    {
        float percent = value * 100f;
        string new_txt = $"{percent:#0.0}";
        new_txt = new_txt.PadLeft(4);
        bar_text.text = new_txt;
    }
}
