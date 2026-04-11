Call SR1.Instrument.CloseForm(10)
FormID = SR1.QuickMeas.FreqResp.OpenFormwID()
FormID = SR1.QuickMeas.OpenFormwID()
Call SR1.QuickMeas.Setup()
Call SR1.Instrument.CloseForm(5)
SR1.QuickMeas.FreqResp.LevelSteps = 199
Call SR1.QuickMeas.FreqResp.Sweep()

Dim i As Integer
For i = 0 To 199
    Call SR1.Displays.Graph(2).SelectTrace(SR1.Displays.Graph(2).Trace(101 + i))
    Call SR1.Displays.Graph(2).ExportData("C:\Documents and Settings\SR1\My Documents\sweep_" & i & ".TXT")
Next i

Call SR1.Displays.Graph(2).Close()
Call SR1.Instrument.CloseForm(2)