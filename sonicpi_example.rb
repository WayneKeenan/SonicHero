live_loop :foo do
  use_real_time
  osc = sync "/osc/bubbleworks/bleguitar"
  L1, L2, L3, U1, U2, U3, strummer, whammy, rotation = osc

  if strummer !=0
    if L1 == 1
      synth :pluck, note: :A
    end

    if L2 == 1
      synth :pluck, note: :F
    end

    if L3 == 1
      synth :pluck, note: :D
    end

    if U1 == 1
      synth :pluck, note: :G
    end

    if U2 == 1
      synth :pluck, note: :E
    end

    if U3 == 1
      synth :pluck, note: :C
    end
  end
end
